

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(ontable c)
(on d a)
(on e d)
(clear c)
(clear e)
)
(:goal
(and
(on b e)
(on c a)
(on d c))
)
)


