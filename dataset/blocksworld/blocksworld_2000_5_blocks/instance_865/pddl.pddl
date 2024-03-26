

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(on b e)
(ontable c)
(on d c)
(on e d)
(clear a)
)
(:goal
(and
(on b d)
(on e a))
)
)


