

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b d)
(ontable c)
(on d e)
(ontable e)
(clear a)
(clear b)
)
(:goal
(and
(on a c)
(on b e)
(on d a)
(on e d))
)
)


