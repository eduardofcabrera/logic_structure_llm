

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b e)
(ontable c)
(on d a)
(on e d)
(clear b)
)
(:goal
(and
(on b e)
(on d b))
)
)


