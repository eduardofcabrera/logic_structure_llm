

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
(on a b)
(on b d)
(on d c)
(on e a))
)
)


