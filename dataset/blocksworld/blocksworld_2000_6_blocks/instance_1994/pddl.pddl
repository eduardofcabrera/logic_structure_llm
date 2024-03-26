

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(ontable c)
(on d a)
(on e c)
(clear b)
(clear d)
)
(:goal
(and
(on a e)
(on b c)
(on c a))
)
)


